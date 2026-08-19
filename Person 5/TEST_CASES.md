# Person 5 - Chatbot Test Cases

Use these questions to test `/chat` after running ingestion and starting Ollama.

| # | Category | Question | Expected behavior |
|---|---|---|---|
| 1 | Products | Which solar panel brands are mentioned? | Mentions product info and cites products.md. |
| 2 | Products | What should I compare before choosing a solar panel? | Mentions wattage, efficiency, warranty, dimensions, price. |
| 3 | Products | Which inverter brands are in the knowledge base? | Mentions inverter/product guidance. |
| 4 | Products | Are lithium batteries better than lead acid? | Explains comparison without unsupported claims. |
| 5 | Sizing | What size solar system do I need for 600 monthly units? | Gives initial estimate and asks for site details. |
| 6 | Sizing | How many panels are needed for a 5 kW system? | Gives approximate panel count based on panel wattage. |
| 7 | Sizing | What is the difference between kW and kWh? | Defines both clearly. |
| 8 | Sizing | How do I estimate monthly solar generation? | Uses planning logic and gives caveats. |
| 9 | Pricing | What is the price of a 5 kW solar system in Pakistan? | Gives approximate range and cites pricing.md. |
| 10 | Pricing | Why do solar prices change? | Mentions exchange rate, brand, city, installation scope. |
| 11 | Pricing | Does adding batteries increase cost? | Explains battery cost impact. |
| 12 | Pricing | Can you give exact quotation for my home? | Says final quotation needs survey/current prices. |
| 13 | Batteries | Do I need batteries for on-grid solar? | Says not usually unless backup/self-consumption needed. |
| 14 | Batteries | How is battery size calculated? | Explains backup load x backup hours x safety factor. |
| 15 | Batteries | What battery details should be checked? | Mentions usable kWh, voltage, chemistry, warranty. |
| 16 | Maintenance | How should I clean solar panels? | Gives safe cleaning guidance. |
| 17 | Maintenance | How often should panels be maintained? | Mentions periodic cleaning/inspection. |
| 18 | Maintenance | What inverter maintenance is needed? | Mentions ventilation, monitoring, safe inspection. |
| 19 | Installation | What happens during a site survey? | Mentions roof, shading, loads, inverter/battery location. |
| 20 | Installation | What info is needed before installation? | Mentions city, bills, loads, roof area, backup. |
| 21 | Installation | Why is shading important? | Explains output loss/design impact. |
| 22 | Warranty | What warranty do solar panels usually have? | Mentions product/performance warranty with caution. |
| 23 | Warranty | What warranty should I check for inverter? | Mentions model-specific warranty/service. |
| 24 | Warranty | Is warranty same for every brand? | Says no, verify model/vendor terms. |
| 25 | Net metering | What is net metering in Pakistan? | Gives safe NEPRA/DISCO answer. |
| 26 | Net metering | What is NEPRA? | Explains authority and current-rule caution. |
| 27 | Net metering | Will solar remove my electricity bill completely? | Says not necessarily; charges/tariffs remain. |
| 28 | Unrelated | Who won the football world cup? | Rejects as non-solar. |
| 29 | Unrelated | Write me a poem about rain. | Rejects as non-solar. |
| 30 | Incomplete | Price? | Asks for clearer solar/system details or gives insufficient info. |
| 31 | Incomplete | Battery? | Asks for backup/load/system context. |
| 32 | Mixed | I use 600 units in Lahore and need 4 hours backup, what system? | Gives initial solar guidance and may recommend using /recommend. |
