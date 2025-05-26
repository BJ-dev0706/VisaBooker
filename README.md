# Visa Booking Automation

An automated tool for visa application booking.

## Project Structure

```
visa-booking-automation/
├── .env                   # Environment variables (create this file)
├── app.py                 # Main application entry point
├── src/                   # Source code directory
│   ├── config/            # Configuration modules
│   │   ├── __init__.py
│   │   └── settings.py    # Environment variables and settings
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   └── browser.py     # Browser utility functions
│   └── services/          # Business logic services
│       ├── __init__.py
│       └── visa_booking.py # Visa booking workflow functions
└── README.md              # Project documentation
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/BJ-dev0706/VisaBooker.git
cd VisaBooker
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:

```
AUTH_EMAIL=your_email@example.com
AUTH_PASSWORD=your_password
USER_FIRST_NAME=YourFirstName
USER_LAST_NAME=YourLastName
USER_BIRTHDAY=01/01/1990
USER_PASSPORT_NUMBER=AB1234567
USER_EXPIRE_DATA=01/01/2030
USER_PHONE_HEADER=1
USER_PHONE_BODY=5551234567
USER_ADDRESS_LINE=123 Main St
DEFAULT_APPLYING_FROM=USA
DEFAULT_GOING_TO=Austria
PROXY=http://your-proxy-if-needed
```

## Usage

Run the application:

```bash
python app.py
```

The application will automatically:
1. Log into the visa application system
2. Navigate to the booking section
3. Fill out personal details
4. Select available appointment dates
5. Complete the booking process

## Requirements

- Python 3.7+
- SeleniumBase
- Dotenv

## Troubleshooting

If you encounter issues:
1. Check your internet connection
2. Verify your credentials in the `.env` file
3. Check that you have the proper browser drivers installed
4. Review logs in `app.log` for specific errors 