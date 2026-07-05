# Personality Generation model used

I have use da three-layer generation model:
Population-level distributions: Define different OCEAN distributions for each persona type (social media user, employee, dark web participant, etc.) based on literature or reasonable assumptions.
Behavior derivation: Generate observable behaviors (posting frequency, browsing frequency, risk tolerance, transaction probability, etc.) from those personality traits using weighted rules or simple functions, rather than assigning them independently.
Instance creation: Instantiate each class using the generated personality and behavior values.