import httpx
import logging
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

async def verify_mc_number(mc_number: str) -> dict:
    """
    Verify a motor carrier number using the FMCSA docket-number lookup.
    """
    # Normalize: strip "MC" or "MC-" prefix, remove spaces
    clean = mc_number.upper().replace("MC-", "").replace("MC", "").strip()
    
    if not clean or not clean.isdigit():
        return {
            "eligible": False,
            "carrier_name": None,
            "status": "INVALID_NUMBER",
            "mc_number": mc_number,
        }

    if not settings.fmcsa_api_key:
        logger.warning("No FMCSA API key configured; cannot verify MC number.")
        return {
            "eligible": False,
            "carrier_name": None,
            "status": "CONFIGURATION_ERROR",
            "mc_number": mc_number,
        }

    # FMCSA auth: webKey passed as query parameter. MC numbers use docket-number lookup.
    url = f"{settings.fmcsa_api_url.rstrip('/')}/docket-number/{clean}"
    params = {"webKey": settings.fmcsa_api_key}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 404:
                logger.info(f"Carrier not found in FMCSA for MC {clean}")
                return {
                    "eligible": False,
                    "carrier_name": None,
                    "status": "NOT_FOUND",
                    "mc_number": mc_number,
                }
            
            response.raise_for_status()
            data = response.json()

            content = data.get("content") or []
            first_match = content[0] if isinstance(content, list) and content else {}
            carrier = first_match.get("carrier") if isinstance(first_match, dict) else {}

            # If carrier block is missing entirely, the number is not in FMCSA
            if not carrier:
                logger.info(f"Carrier data empty in FMCSA response for MC {clean}")
                return {
                    "eligible": False,
                    "carrier_name": None,
                    "status": "NOT_FOUND",
                    "mc_number": mc_number,
                }
            
            allowed = carrier.get("allowedToOperate", "N")
            name = carrier.get("legalName") or carrier.get("dbaName") or "Unknown"
            
            return {
                "eligible": allowed == "Y",
                "carrier_name": name,
                "status": "ACTIVE" if allowed == "Y" else "INACTIVE",
                "mc_number": mc_number,
            }
    except httpx.HTTPStatusError as e:
        logger.error(f"FMCSA HTTP error {e.response.status_code}: {e.response.text}")
        return {
            "eligible": False,
            "carrier_name": None,
            "status": "LOOKUP_ERROR",
            "mc_number": mc_number,
        }
    except Exception as e:
        logger.error(f"FMCSA API call failed: {e}")
        return {
            "eligible": False,
            "carrier_name": None,
            "status": "LOOKUP_ERROR",
            "mc_number": mc_number,
        }
