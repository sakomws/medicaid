# platgpt

PHI stands for Protected Health Information and it includes data elements that can be used within a data set to identify an individual and disclose their medical records and/or health related financial history.


Fine tune model:
base_model: accounts/fireworks/models/mixtral-8x7b-instruct

Medicaid Dataset: goup/medicaid
https://huggingface.co/datasets/goup/medicaid/blob/main/Medicaid_Application_Form_Synthetic_Data.jsonl

```
curl https://storage.googleapis.com/fireworks-public/firectl/stable/darwin-arm64.gz -o firectl.gz
gzip -d firectl.gz && chmod a+x firectl
sudo mv firectl /usr/local/bin/firectl
sudo chown root: /usr/local/bin/firectl
```

```
firectl create fine-tuning-job --settings-file settings.yaml --display-name "HIPAA Completion"
```

curl \
  -H "Authorization: Bearer ${FIREWORKS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "accounts/sahriyarm-b6065d/models/1bc4ef642865488692d371896b7aebc2", "prompt": "Is the applicant enrolled in any health insurance?"}' \
  https://api.fireworks.ai/inference/v1/completions


curl \
  -H "Authorization: Bearer ${FIREWORKS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "accounts/fireworks/models/mixtral-8x7b-instruct",  "max_tokens": 4096, "prompt": "What is the annual income of the applicant?"}' \
  https://api.fireworks.ai/inference/v1/completions

## Dataset in HuggingFace
https://huggingface.co/datasets/goup/medicaid/blob/main/Medicaid_Application_Form_Synthetic_Data.jsonl



## Resources
https://github.com/microsoft/presidio-research/blob/master/docs/requirements/industry/hipaa/source-material.md
https://www.hipaajournal.com/hipaa-compliance-checklist
https://github.com/a16z-infra/llm-app-stack/tree/main
https://github.com/globerhofer/HIPAA-policies
https://readme.fireworks.ai/docs/fine-tuning-models
