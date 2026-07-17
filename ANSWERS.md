# MedNorth Take-Home Assessment - Answers

## Part 2: Source mapping and assumptions

### 1. Source-to-JAF Field Mapping

**MedNorth EMR (CSV):**
- `Record_ID` -> `external_id`
- `Full_Name` -> split by space or comma into `first_name` and `last_name`
- `DOB` -> `date_of_birth` (normalized as ISO 8601)
- `Email` -> `email` (converted to lowercase and trimmed)
- `Phone` -> `phone` (formatted to E.164)
- `Hire_Date` -> `hire_date` (normalized to ISO 8601)
- `Dept_Code` -> `department` (mapped by dict)
- `City_State` -> split by comma or hyphen into `city` and `state`
- `Active_Flag` -> `status` (mapped to ACTIVE / INACTIVE)

**PeopleFlow HRIS (JSON):**
- `employee_number` -> `external_id`
- `name.first` / `name.last` -> `first_name` / `last_name`
- `birth_date` -> `date_of_birth` (normalized to ISO 8601)
- `contact.email` -> `email`
- `contact.mobile` -> `phone`
- `start_date` -> `hire_date` (normalized to ISO 8601)
- `department` -> `department`
- `address.city` / `address.state` -> `city` / `state`
- `employment_status` -> `status` ("leave of absence" mapped to ACTIVE, "terminated" to INACTIVE)

### 2. Data Treatment
* **Ambiguous date:** I used the `dateutil.parser` lib to parse dates dynamically. In ambiguous cases ("04-05-2023"), I chose to keep the American notation (MM-DD-YYYY) because the source of the data is American (Texas cities).
* **Unmapped Department:** Since the department is required and the department was unmapped, it wasn't possible to classify it, so I created a rejected queue to store that data and explain why the entry was rejected. In the rejected Queue, the entries can be analyzed and reprocessed.
* **Within-source duplicate:** I used `drop_duplicates(subset=['Email'], keep='first')` after cleaning the data, using the email as the primary key. If the source has two entries for the same email, only the first will be used for the merge.

### 3. Merge Rule and Conflict Resolution
To merge data from different sources, I used the Email field as the primary key. I used the Pandas `combine_first()` function, prioritizing data coming from the HR System (PeopleFlow HRIS JSON). The choice is based on the premise that the HR system would be the official and most up-to-date source of truth for employee data. The EMR data was only used to fill in empty fields.

### 4. Customer Onboarding questions
1. Which source is more reliable to be used as the source of truth in case of conflicting data? 
2. What is the official regional date format used in internal systems? We need this information to treat possible ambiguous dates.
3. What should be done when employees arrive without required fields? Should we store them in a rejection file or insert them with generic data like 'No Department'?

---

## Part 3: Short answer

**[Original Text in Portuguese for Practice]**

**1. Intermittent overnight timeout failures:**
I would check the traffic patterns, maybe some infrastructure maintenance, or if they are running other routines like synchronizations or backups. These processes can overload servers or lock tables, slowing the process and causing the timeout error.

**2. Resilient web scraper design:**
If the page structure occasionally changes, I think it's better to look for stable elements. I would avoid using generic CSS classes, and instead use semantic identifiers or accessibility labels.
To know when the scraper breaks, it's important to implement validations like using Pydantic to raise an error if the data doesn't match with the correct type.
**3. Handling unexpected HR status values:**
The goal would be to align on the business rule with the customer success team and understand what these statuses imply. If I need to continue processing before this definition, I would store this 'wrong' data in the rejected Queue for later processing.
---