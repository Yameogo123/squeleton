
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
    