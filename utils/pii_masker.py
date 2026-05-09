from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def mask_pii(text):
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    # Analyze for specific sensitive entities
    results = analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON"], language='en')
    
    # Anonymize with placeholders
    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized_result.text