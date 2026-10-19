import os


class Utils:
    @staticmethod
    def not_in_env(env: str) -> bool:
        """
        Check if an environment variable is not set (or empty).

        Examples:
            >>> Utils.not_in_env("PATH")
            False
            >>> Utils.not_in_env("NON_EXISTENT_VAR")
            True
        """
        return not os.getenv(env)

    @staticmethod
    def not_all_in_env(envs: list[str]) -> bool:
        """
        Check if at least one of the environment variables is not set.

        Examples:
            >>> Utils.not_all_in_env(["PATH", "NON_EXISTENT_VAR"])
            True
            >>> Utils.not_all_in_env(["PATH", "HOME"])
            False
        """
        return any(Utils.not_in_env(env) for env in envs)
