def time_in_ms(mytime):
    """
        Convert time to milliseconds to interact with the Feedly API
        
        Parameters
        ----------
        mytime : datetime.datetime
            datetime

        Returns
        -------
        int
            time in milliseconds

    """
    return int(mytime.microsecond*1e3)