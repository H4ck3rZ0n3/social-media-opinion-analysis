# topic_effectiveness_classifier.py

class TopicEffectivenessClassifier:
    @staticmethod
    def classify_topic_effectiveness(comments):
        if not isinstance(comments, list):
            raise ValueError("Input should be a list of dictionaries.")

        for comment in comments:
            if not isinstance(comment, dict) or 'type' not in comment:
                raise ValueError("Each comment must be a dictionary with a 'type' key.")

        claim_count = sum(1 for c in comments if c.get('type') == 'Claim')
        counter_count = sum(1 for c in comments if c.get('type') in ['Counterclaim', 'Rebuttal'])

        if claim_count > counter_count:
            return "Effective"
        elif claim_count == counter_count:
            return "Adequate"
        else:
            return "Ineffective"
