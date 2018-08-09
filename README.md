# Project 3

## Proposal
The purpose of this project is to analyze Texas hospital discharge data from 2011 and to evaluate the subset of patients who have experienced cardiac arrest, and to build a binary classifier that predicts if a patient is alive or dead at the time of discharge, depending on their demographics and other associated diagnoses or procedure codes.

## Domain
I have experience in health care, which will help in evaluating the features that are present in the data set and which ones could be potentially relevant. There is also fairly extensive medical literature about the question of likelihood of survival after cardiac arrest, but I am interested in seeing what the relative importance is of different predictors, e.g. whether or not it matters whether or not the patient is at an academic hospital or not, etc.

## Data
The data I am planning on using is from Texas's publicly available [hospital discharge data sets](https://www.dshs.texas.gov/THCIC/Hospitals/Download.shtm). The most recent year that is available is 2011, so I plan to use the data from this year and to pull the subset of patients who have the diagnosis code for cardiac arrest in their record (patients can have ~20 diagnosis codes associated with their hospital stay), and to analyze this subset.

The target variable is the patient status at time of discharge, either expired (or discharged to hospice), or alive. If I have time, I may turn this into a multiclass classifier, splitting it into 1) expired or discharged to hospice, 2) discharged to skilled nursing facility or acute inpatient rehabilitation, or 3) discharged home or to home care; these 3 classes are relevant since there is a clear clinical difference between patients who are well enough to be discharged home and patients who have to be discharged to a rehabilitation facility. It's possible that the number of people who are able to be discharged home will be too small for the model to train on, so multiclass classification may not work as well as binary.

The predictor variables will broadly fall into the following categories:

### Personal demographics
* Age
* Gender
* Race
* Ethnicity
* Primary payer (Medicare, Medicaid, private insurance, etc.)
* Patient zip code/county

### Details about hospital stay
* Day of the week patient admitted (difference between mortality in patients admitted on weekday vs weekend?)
* Type of hospital patient is admitted to; academic vs private vs community vs critical access hospitals
* Length of stay
* Type of admission (urgent vs emergent vs elective)
* Source of admission

### Medical/procedural
* In-hospital vs out-of-hospital cardiac arrest (presumably, patients who had an admitting diagnosis of cardiac arrest experienced their arrest out-of-hospital, although there may be inaccuracy here if the patient was transferred from another hospital; need to account for this by looking at the source of admission)
* Other associated diagnosis codes, e.g. diabetes, heart failure, etc.
* Other associated procedural codes, e.g. heart surgery, mechanical ventilation, etc.

For the associated medical and procedural diagnosis codes, it probably makes the most sense to find the top 5-10 most common diagnosis codes for each and then to use these as dummy variables, since there are thousands of diagnosis codes, and the contribution of the less common ones to a model is probably negligible and not worth the hassle of turning all of them into dummy variables.

## Known unknowns
I'm not sure how complete or clean the data is; the data is located in tab-delimited files, one for each quarter of 2011. I looked at the first quarter's spreadsheet, and it contains ~700K records. My first queries showed that there about 800 records for patients who had an admitting diagnosis of cardiac arrest, and about 3000 records for patients who had cardiac arrest listed anywhere in their record.

I think it's certainly possible that the model will end up selecting features that are fairly obvious, e.g. age and certain other comorbidities are very strong predictors for mortality at time of discharge. I think there are a few things that could be potentially interesting, e.g. seeing if hospital type or primary payer (which is a marker of patient socioeconomic status) has a strong influence.

It would also be interesting to see if my model replicates the statistics in the published literature regarding mortality of cardiac arrest. The other thing that could be interesting to look at would be how a model trained on the data for 2011 ends up performing on data for 2010, or 2009; if the classifier has higher Type 1 error (e.g. predicts people dying when they survive) for previous years, does this mean people are getting sicker overall? Or does it mean that medical care is getting worse? You would hope that a binary classifier for mortality rate would have higher Type 2 error as the years go on, since it would hopefully mean that people would be surviving more when previously they would not have been expected to.

Finally, if I am able to build a robust pipeline for the data, it should actually be fairly easy to query the dataset for any diagnosis code of interest, e.g. pneumonia, heart attack, etc. Looking at the accuracy of models for patients who have these diagnoses and what the important predictors are for these other diagnoses could also be interesting.
