--
-- PostgreSQL database dump
--

\restrict SMwJH2f57NdGw2XCygSkU7gM1j7BIFxWLead39rGxVj35YvYBMU3MHNz9WFqUIL

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

TRUNCATE TABLE public.call_records RESTART IDENTITY;

--
-- Data for Name: call_records; Type: TABLE DATA; Schema: public; Owner: happyrobot
--

INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('e42a6f12-7203-44c0-970f-d2f22f2aaa58', '8e8a80b0-72f6-4fc7-8dda-1fe6214c2b78', '1234567', 'ARTHUR J KENYON', 'LD-12345', 'Houston, TX', 'New Orleans, LA', 'Dry Van', 1100, 1000, 'dropped', 'negative', 0, NULL, NULL, 'I can’t summarize because the transcript appears to be empty. Please paste the transcript text (or upload the file) and tell me any preferences. For example:

- Desired length: one-sentence, short paragraph, bullet list, or detailed summary
- Tone: neutral, executive, casual
- Include: timestamps, action items, key quotes, speakers’ names

If helpful, here are three example summary templates you can choose from once you provide the transcript:

1) One-line executive summary
- Single sentence capturing the main outcome or decision.

2) Short bullets (3–6 bullets)
- Main topic
- Key decisions or conclusions
- Top 2–3 action items with owners and due dates (if present)

3) Detailed summary (several paragraphs)
- Meeting purpose and participants
- Discussion points by topic
- Decisions and rationale
- Complete action-item list (owner + deadline)
- Important quotes or references + timestamps

Share the transcript and your preferred template/length and I’ll produce the summary.', true, false, '2026-06-05 21:59:08.699437');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('57be30ca-dd5a-42d0-9def-0fccfbd9a505', '82d77830-8460-4f74-89e4-0cf1701a063e', '123343', 'DHL EXPRESS USA INC', 'LD-10005', 'Houston', 'New Orleans', 'Dry Van', 1140, 1037, 'agreed', 'positive', 139, NULL, NULL, 'Caller (DHL Express USA Inc, MC 123343) with a tri-van in Houston booked a Dry Van load to New Orleans (pickup Jun 7, 07:00; delivery Jun 8, 09:00; 350 miles, LD-10005). Listed $1,037 negotiated to $1,140; call transferred to sales for booking.', true, false, '2026-06-05 22:09:31.634969');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('0c3f61f4-c7a2-452d-ad6d-685e3994e136', '8d6f8f74-76df-4018-8b17-c4121408e9f2', '123343', 'DHL EXPRESS USA INC', 'LD-10003', 'Seattle, WA', 'Portland, OR', 'Dry Van', 530, 483.42, 'agreed', 'positive', 139, NULL, NULL, 'Carrier from DHL EXPRESS USA INC with MC 123343 accepted a dry van load from Seattle, WA to Portland, OR. Original rate was $483.42, negotiated to $530. Pickup is on June 7th. Transferred to sales rep for finalization.', true, false, '2026-06-05 22:33:48.788703');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('b68ff172-082a-4dd2-be4d-948c7b61680f', '2b5b1ec9-2d58-41da-bd67-c1f668c3da01', '678124', 'TIMOTHY O COCHRAN', NULL, 'Chicago, Illinois', 'Milwaukee', 'Dry Van', NULL, NULL, 'no_match', 'positive', 72, NULL, NULL, 'Carrier Timothy O Cochran (MC 678124) called looking for dry van loads from Chicago, IL to Milwaukee. No loads were available at this time.', true, false, '2026-06-05 22:35:55.255271');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('cfea0110-03d9-4a2c-b902-1487603ef599', '56a34d87-0f77-40ac-80f8-e9c30e956fe9', '918271', 'JEFFERY L PROSS', NULL, 'Houston, Texas', 'New Orleans, Louisiana', 'Dry Van', NULL, NULL, 'no_match', 'positive', 125, NULL, NULL, 'Carrier JEFFERY L PROSS (MC 918271) called to check for dry van loads from Houston, TX to New Orleans, LA. No loads were available. Carrier declined to check other destinations.', true, false, '2026-06-05 22:38:41.246468');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('bb893e34-a832-4155-956a-ad61eec0265a', '9f7a14ec-1653-48b1-98b7-35946662de8a', '999999', 'TLA TRUCKING LLC', 'LD-10001', 'Atlanta, GA', 'Charlotte, NC', 'Dry Van', 750, 681.22, 'agreed', 'positive', 119, NULL, NULL, 'Carrier from TLA Trucking LLC (MC 999999) accepted a dry van load from Atlanta, GA to Charlotte, NC. Original rate was $681.22, negotiated up to $750. Load ID: LD-10001.', true, false, '2026-06-05 22:41:43.537937');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('25960da7-7b0e-4ad5-842b-deb220ae2e71', '8d5a82ba-3830-459f-ad0b-39a778ba6b10', '123343', 'DHL EXPRESS USA INC', 'LD-10014', 'Denver, CO', 'Salt Lake City, UT', 'Flatbed', 1300, 1190, 'agreed', 'positive', 114, NULL, NULL, 'Carrier from DHL Express USA Inc booked a flatbed load from Denver, CO to Salt Lake City, UT. Original rate was $1,190, negotiated to $1,300. Pickup is June 5th. MC number 123343.', true, false, '2026-06-05 22:54:07.040874');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('4119e99b-0e31-431c-859e-028c239d4652', '5ad54317-51df-495c-b3df-2f2b3fe3ee5e', '123343', 'DHL EXPRESS USA INC', 'LD-10019', 'Seattle, WA', 'Portland, OR', 'Step Deck', 655, 595, 'agreed', 'positive', 99, NULL, NULL, 'Carrier DHL EXPRESS USA INC booked a Step Deck load from Seattle, WA to Portland, OR for June 8th. Original rate was $595, negotiated to $655. Load ID: LD-10019.', true, false, '2026-06-05 23:09:34.023075');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('d254e641-6501-4897-ad3d-183d1cb79ae1', '97c375a2-ce92-4479-9115-df56f539bbf8', '123343', 'DHL EXPRESS USA INC', NULL, 'Seattle, Washington', 'Portland', 'Dry Van', NULL, NULL, 'no_match', 'neutral', 69, NULL, NULL, 'Carrier DHL EXPRESS USA INC (MC 123343) called to book a load from Seattle, WA to Portland with a Dry Van. No loads were available for this lane at the time of the call.', true, false, '2026-06-05 23:42:58.982948');
INSERT INTO public.call_records (id, run_id, mc_number, carrier_name, load_id, origin, destination, equipment_type, agreed_rate, initial_rate, outcome, sentiment, duration_seconds, started_at, ended_at, summary, loads_found, call_dropped, created_at) VALUES ('13b582da-bf46-4186-895c-a54e5bccfe8b', 'cb291e6d-5d16-4439-8380-87eca5895502', '123343', 'DHL EXPRESS USA INC', 'LD-10019', 'Seattle, WA', 'Portland, OR', 'Step Deck', 655, 595, 'agreed', 'positive', 103, NULL, NULL, 'Carrier DHL EXPRESS USA INC (MC 123343) booked a step deck load from Seattle, WA to Portland, OR. Original rate was $595, negotiated to $655. Pickup is June 8th. Carrier accepted the offer and will be transferred to sales to finalize.', true, false, '2026-06-05 23:48:22.025458');


--
-- PostgreSQL database dump complete
--

\unrestrict SMwJH2f57NdGw2XCygSkU7gM1j7BIFxWLead39rGxVj35YvYBMU3MHNz9WFqUIL
