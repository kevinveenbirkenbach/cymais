class FilterModule(object):
    def filters(self):
        return {
            'get_public_id': self.get_public_id
        }

    def get_public_id(self, value):
        """
        Extract the substring after the last hyphen in the input string.
        Example:
          'service-user-abc123' => 'abc123'
        """
        if not isinstance(value, str):
            raise ValueError("Expected a string")
        if '-' not in value:
            raise ValueError("No hyphen found in input string")
        return value.rsplit('-', 1)[-1]
