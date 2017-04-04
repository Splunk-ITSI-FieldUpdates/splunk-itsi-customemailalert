# splunk-itsi-customemailalert
This custom email alert action sends a single email with configurable parameters (username/password/recipient/email text) and attaches all entities available in the KPIs from the initial multi-kpi alert with their current state. This email allows administrators to quickly identify faulty entities and streamline the initial investigation.

Required libraries:
	splunk sdk (current version)
	requests (2.7 or higher)
