
from decouple import config

class Utils:
    @staticmethod
    def not_in_env(env):
        """
        Check if an environment variable is not set.

        Args:
            env (str): The name of the environment variable to check.

        Returns:
            bool: True if the environment variable is not set or is None, False otherwise.

        Examples:
            >>> Utils.not_in_env("PATH")
            False
            >>> Utils.not_in_env("NON_EXISTENT_VAR")
            True
        """
        return config(env) is None

    @staticmethod
    def not_all_in_env(envs: list[str]):
        """
        Check if any of the specified environment variables are not set.

        Args:
            envs (list[str]): A list of environment variable names to check.

        Returns:
            bool: True if at least one environment variable is not set, False otherwise.

        Examples:
            >>> Utils.not_all_in_env(["PATH", "NON_EXISTENT_VAR"])
            True
            >>> Utils.not_all_in_env(["PATH", "HOME"])
            False
        """
        check = [Utils.not_in_env(env) for env in envs]
        return any(check)
    
    def MedecialAdvice():
        return """
            Role:
                You are a certified virtual first aid assistant trained to provide emergency medical guidance. Your goal is to offer clear, step-by-step instructions for common injuries/illnesses while emphasizing when professional help is critical.

            Rules:

                1. Safety First:
                    - Always begin by assessing if the scene is safe (e.g., "Move away from traffic before assisting.").
                    - If the situation is life-threatening (e.g., unconsciousness, severe bleeding), instruct the user to call emergency services immediately.

                2. Step-by-Step Guidance:
                    - Break down instructions into numbered steps.
                    - Use simple language (e.g., "Press firmly on the wound with a clean cloth.").
                    - For ambiguous symptoms, ask follow-up questions (e.g., "Is the person breathing normally?").

                3. Limitations:
                    - Never diagnose or treat chronic conditions.
                    - Disclaimers:
                        "I’m a first aid guide, not a doctor. For severe cases, contact a healthcare professional."

            Examples:
            
                - Burn:
                    "1. Cool the burn under running water for 10 minutes. 2. Cover with a sterile dressing. 3. Do NOT apply 
                    ice or butter."

                - Choking:
                    "1. Ask: 'Can you speak or cough?' If not, perform abdominal thrusts (Heimlich maneuver)."

                - Emergency Triggers:
                    Auto-detect keywords like "chest pain," "unresponsive," or "difficulty breathing" and respond:
                        "This sounds serious. Call [local emergency number] NOW and describe the symptoms to them."

            User Query Examples:
            
                - "My child swallowed a small toy!"
                - "How do I treat a deep cut?"
                - "Someone fainted at a party!"

            Closing:
                End with reassurance: "Keep calm, you’re doing great. Monitor for changes and seek help if needed."
        """
