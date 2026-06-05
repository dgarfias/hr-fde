# HappyRobot Workflow Configuration

This document describes how to build the **Inbound Carrier Sales** workflow inside the HappyRobot platform UI. You cannot version-control the workflow itself (it lives in HappyRobot), but this guide is your build spec.

## Prerequisites

- HappyRobot account with access to Voice Agents and Workflows
- API key for the external API (generated from your deployed dashboard or set in env)
- Your API deployed and reachable over HTTPS (e.g. `https://hr.garfias.dev`)

## Workflow Overview

```
[Inbound Phone Call Trigger]
         │
         ▼
[Inbound Voice Agent Prompt]
   ├── Tool: VerifyMC ──▶ Webhook ──▶ POST /fmcsa/verify
   ├── Tool: SearchLoads ──▶ Webhook ──▶ GET /loads
   ├── Tool: MockTransfer ──▶ Webhook ──▶ POST /offers
   └── Tool: RecordCounterOffer ──▶ Webhook ──▶ POST /offers (draft)
         │
         ▼
[AI Extract] ──▶ Extract offer fields from transcript
         │
         ▼
[AI Classify] ──▶ Outcome tag (price_agreed, declined, ...)
         │
         ▼
[AI Classify] ──▶ Sentiment tag (positive, neutral, negative)
         │
         ▼
[Webhook] ──▶ POST /offers (final structured record)
```

## Step-by-Step Build

### 1. Create the Workflow

1. Go to **platform.happyrobot.ai** → Workflows → **New Workflow**
2. Name: `Inbound Carrier Sales`
3. HappyRobot auto-generates a slug (e.g. `inbound-carrier-sales-V1StGX`). Note it.

### 2. Add Trigger

1. Click **Add Trigger**
2. Select **Inbound Phone Call**
3. Do **not** purchase a number. Instead, this workflow will be triggered via the **Web Call** (browser voice) integration.
4. The trigger provides variables like `@trigger.caller_number` and `@trigger.called_number`.

### 3. Add the Inbound Voice Agent

1. Click **+** after the trigger → **Voice Agent** → **Inbound Voice Agent**
2. Configure:
   - **From**: Leave as default (web call does not require a purchased number)
   - **Model**: `GPT-4.1` or `GPT-5` (recommended for complex negotiation)
   - **Voice**: Pick a professional voice (e.g. `Sarah` or `Alex`)
   - **No initial message**: **Disabled** (the agent should greet first)

3. **Prompt** (copy-paste exactly):

```
You are Alex, an inbound carrier sales representative at Acme Logistics.

Objective: Help carriers book loads by verifying their MC number, matching them to available freight, and negotiating rate.

Instructions:
1. Greet the carrier professionally and ask for their MC number.
2. Use the VerifyMC tool to validate eligibility via FMCSA.
3. Qualify the carrier's current situation. Ask naturally where their truck is sitting empty right now, where they are trying to head, and what type of equipment they are running. Do not say "what lane and equipment type are you looking for?" — that sounds like a phone tree.
4. Use the SearchLoads tool with the carrier's current location, desired destination, and equipment type to find the best available match.
5. The tool returns a single flat object (same pattern as VerifyMC) with a `loads` array inside. Check the `found` field. If `found` is true, read the first load from `loads[0]` and pitch it: origin, destination, pickup date, listed rate, miles, and equipment type. Ask if it works for them. If the carrier asks for alternatives or says no, you may read `loads[1]` or `loads[2]` if they exist. Do not read more than 3 loads total.
6. Ask if they are interested in accepting the load at the listed rate.
7. If they make a counter-offer, negotiate up to 3 back-and-forth rounds. Stay within 10% of the loadboard_rate floor.
8. If you reach agreement, use the MockTransfer tool to "transfer" to a human sales rep.
   - Pass the `carrier_name` you received from the VerifyMC tool earlier in the call.
   - Say: "Transfer was successful and now you can wrap up the conversation."
9. If they decline after negotiation, thank them and end politely.

Rules:
- Do not disclose customer names or sensitive shipper information.
- Keep negotiations concise; do not exceed 3 rounds.
- Always confirm the final agreed rate before the mock transfer.
- If the caller is confused, repeat the load details once, then offer to transfer.
- If the caller is hostile or uncooperative, remain professional and offer to transfer.
- If the SearchLoads tool returns `found` as false, tell them honestly that you don't have anything in that lane right now, but ask if you can call them back when something opens up. Do not make up fake loads.
```

4. **Initial message** (outbound) and **Receiving initial message** (inbound):
   - Inbound: `Hi, thanks for calling Acme Logistics. I'm Alex, your automated carrier sales assistant. To get started, may I have your MC number?`

> **Demo Test Script:** When testing the web call, say: *"My MC number is 150768. I'm sitting empty in Houston with a Dry Van and I'm trying to get down to New Orleans."* This will match the Houston → New Orleans load in our demo board.

### 4. Attach Tools to the Voice Agent

Click **+** below the prompt node to add tools. Each tool is a child of the prompt.

#### Tool A: VerifyMC

- **Description**: `Use this tool when the caller provides their MC number. It validates carrier eligibility through the FMCSA database.`
- **Message**: `Let me verify that MC number for you.` (Fixed message)
- **Parameters**:
  - `mc_number` (string) — The motor carrier number provided by the caller.
- **Child Action**:
  1. **Webhook** → Method: `POST`, URL: `https://<YOUR_DOMAIN>/fmcsa/verify`
     - Headers: `Authorization: Bearer <API_KEY>`, `Content-Type: application/json`, `client: happy-robot`
     - Body: `{ "mc_number": "@tool.parameters.mc_number" }`

> **Note on branching**: Instead of adding Conditionals nodes to the workflow, handle all VerifyMC responses **inside the prompt** (see step 3). The voice agent reads the tool's JSON response and decides what to say next. This keeps the workflow graph simple.

**Expected response shapes:**

Verified carrier:
```json
{
  "eligible": true,
  "carrier_name": "DEALERS TRUCK EQUIPMENT",
  "status": "ACTIVE",
  "mc_number": "150768"
}
```

Not found:
```json
{
  "eligible": false,
  "carrier_name": null,
  "status": "NOT_FOUND",
  "mc_number": "999999999"
}
```

#### Tool B: SearchLoads

- **Description**: `Use this tool when the caller specifies where their truck is, where they want to go, and what equipment they run. It searches available loads from our system.`
- **Message**: `Let me pull up available loads for you.` (Fixed message)
- **Parameters**:
  - `origin` (string) — City or state where the truck is currently empty. Example: "Houston"
  - `destination` (string) — City or state the carrier wants to reach. Example: "New Orleans"
  - `equipment_type` (string) — Equipment type. Must be one of the exact values below. If the caller uses a synonym, map it to the canonical value before calling this tool.
    - Valid values: `Dry Van`, `Reefer`, `Flatbed`, `Step Deck`, `Power Only`
    - Common mappings: "van" or "dryvan" → `Dry Van`; "refrigerated" or "reefer" → `Reefer`; "flat bed" → `Flatbed`; "stepdeck" or "step-deck" → `Step Deck`
- **Child Action**:
  1. **Webhook** → Method: `GET`, URL: `https://<YOUR_DOMAIN>/loads/match?origin={{origin}}&destination={{destination}}&equipment_type={{equipment_type}}`
     - Headers: `Authorization: Bearer <API_KEY>`, `client: happy-robot`
  2. The JSON response is returned to the agent as a single flat object (same pattern as VerifyMC) with a `loads` array inside. The agent checks the `found` boolean, then reads from `loads`.

  **Expected response shapes:**

  Match found:
  ```json
  {
    "found": true,
    "count": 2,
    "loads": [
      {
        "load_id": "LD-10005",
        "origin": "Houston, TX",
        "destination": "New Orleans, LA",
        "pickup_datetime": "2026-06-07T07:00:00",
        "delivery_datetime": "2026-06-08T09:00:00",
        "equipment_type": "Dry Van",
        "loadboard_rate": 1037.0,
        "miles": 350
      },
      {
        "load_id": "LD-10013",
        "origin": "Houston, TX",
        "destination": "New Orleans, LA",
        "pickup_datetime": "2026-06-06T03:00:00",
        "delivery_datetime": "2026-06-07T16:00:00",
        "equipment_type": "Reefer",
        "loadboard_rate": 755.47,
        "miles": 350
      }
    ]
  }
  ```

  No match:
  ```json
  {
    "found": false,
    "count": 0,
    "loads": []
  }
  ```

#### Tool C: MockTransfer

- **Description**: `Use this tool when a price has been agreed upon and the caller needs to be transferred to a human sales rep to finalize the booking.`
- **Message**: `Great, we have a deal. Let me transfer you to a sales rep to wrap this up.` (Fixed message)
- **Parameters**:
  - `agreed_rate` (number)
  - `load_id` (string)
  - `mc_number` (string)
  - `carrier_name` (string) — The carrier name returned by the VerifyMC tool earlier in the conversation
- **Child Action**:
  1. **Webhook** → Method: `POST`, URL: `https://<YOUR_DOMAIN>/offers`
     - Headers: `Authorization: Bearer <API_KEY>`, `client: happy-robot`, `Content-Type: application/json`
     - Body:
       ```json
       {
         "call_id": "@trigger.run_id",
         "mc_number": "@tool.parameters.mc_number",
         "carrier_name": "@tool.parameters.carrier_name",
         "load_id": "@tool.parameters.load_id",
         "agreed_rate": "@tool.parameters.agreed_rate",
         "outcome": "price_agreed"
       }
       ```
  2. Since this is a web call (not a real phone line), we **mock** the transfer. Add a **Message** node after the webhook:
     - `Transfer was successful and now you can wrap up the conversation.`

#### Tool D: RecordCounterOffer (optional but recommended)

- **Description**: `Use this tool whenever the carrier makes a counter-offer during price negotiation. It logs the round for analytics.`
- **Message**: None (silent)
- **Parameters**:
  - `offer_rate` (number)
  - `round` (number, 1-3)
- **Child Action**:
  - You can skip a webhook here and rely on the transcript extraction later, or post to a lightweight logging endpoint if you built one.

### 5. Post-Call Processing (After the Voice Agent)

After the voice agent node, add these core nodes in sequence:

#### Node: AI Extract

- **Input**: `@voice_agent.transcript` (the full conversation transcript)
- **Extraction mode**: `Parameters mode`
- **Parameters**:
  - `mc_number` — string
  - `carrier_name` — string
  - `load_id` — string
  - `agreed_rate` — number
  - `negotiation_rounds` — number
  - `origin` — string
  - `destination` — string
  - `equipment_type` — string

#### Node: AI Classify — Outcome

- **Input**: `@voice_agent.transcript`
- **Tags**:
  - `price_agreed`
  - `declined`
  - `callback_requested`
  - `not_eligible`
- **Output**: String tag.

#### Node: AI Classify — Sentiment

- **Input**: `@voice_agent.transcript`
- **Tags**:
  - `positive`
  - `neutral`
  - `negative`
- **Output**: String tag.

#### Node: Webhook — Finalize Offer

- Method: `POST`
- URL: `https://<YOUR_DOMAIN>/offers`
- Headers: `Authorization: Bearer <API_KEY>`
- Body:
  ```json
  {
    "call_id": "@trigger.run_id",
    "mc_number": "@ai_extract.mc_number",
    "carrier_name": "@ai_extract.carrier_name",
    "load_id": "@ai_extract.load_id",
    "agreed_rate": "@ai_extract.agreed_rate",
    "negotiation_rounds": "@ai_extract.negotiation_rounds",
    "outcome": "@ai_classify_outcome.output",
    "sentiment": "@ai_classify_sentiment.output",
    "origin": "@ai_extract.origin",
    "destination": "@ai_extract.destination",
    "equipment_type": "@ai_extract.equipment_type",
    "transcript_summary": "@voice_agent.transcript"
  }
  ```

### 6. Testing

1. **Generate a test record**: Send a test POST to the version-specific test URL shown in the trigger panel. For web call testing, use the **Voice Call Token** endpoint from your backend or the HappyRobot SDK.
2. **Use the Prompt Playground**: Click **Chat Playground** in the prompt editor to verify the agent's behavior before making real calls.
3. **Test each tool**: Use the tool test panel to verify the webhook URLs, headers, and response shapes.
4. **Run end-to-end**: Trigger a web call from your browser UI. Walk through the script as the interviewer (carrier). Review the run transcript and node outputs.

### 7. Publish

1. Once tests pass, click **Publish** → select **Production** environment.
2. The workflow is now live. Web call tokens will route to this published version.
3. Copy the workflow URL from the browser address bar for your deliverables.

## HappyRobot Docs References Used

- **Workflows Overview**: Workflows are a visual graph of nodes executing in sequence; data flows via `@` variables.
- **Triggers**: Inbound Phone Call trigger connects the caller to the workflow immediately.
- **Voice Agents / Prompts and Tools**: Prompt node defines behavior; tools pause conversation, execute child actions (webhooks), and return results.
- **AI Extract**: Pulls structured data from transcripts using parameters mode.
- **AI Classify**: Sorts text into predefined tags (used for outcome and sentiment).
- **Webhook Core Node**: Calls external APIs with custom headers and body templates.
- **Quickstart**: Pattern of Trigger → Voice Agent → AI Extract → publish.
