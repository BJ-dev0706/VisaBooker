from seleniumbase import SB
import logging

from src.config.settings import validate_env_vars
from src.services.visa_booking import (
    login, book_appointment, your_details, book_appointment_data,
    services, review, confirmation, dashboard
)

logger = logging.getLogger(__name__)

def main() -> None:
    """Main application entry point."""
    try:
        validate_env_vars()
        
        with SB(uc=True, incognito=True) as sb:
            login(sb)
            book_appointment(sb)
            your_details(sb)
            book_appointment_data(sb)
            services(sb)
            review(sb)
            confirmation(sb)
            dashboard(sb)
            
        logger.info("Visa booking automation completed successfully.")
    except Exception as e:
        logger.error(f"Error in visa booking automation: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 