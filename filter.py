

def kalman(observation, uncertainty, model, proc_var = [10., 10., 1., 1.], obs_var = [100., 100., 100., 100.]):
    """
    Uses the Kalman filter to infere the 'model' states from the
    'observation'.  The parameters 'proc_var' and 'obs_var' determine
    the speed of the filter adaptations.

    model -- state estimate 
    uncertainty -- state uncertainty
    proc_var -- process variance (left/right variance is larger than depth variance by default)
    obs_var -- observational variance

    """
    for i in range(4):
        # kalman gain
        K              = (uncertainty[i] + proc_var[i]) / (uncertainty[i] + proc_var[i] + obs_var[i]) 
        model[i]       = model[i] + K * (observation[i] - model[i])      # updated state estimate
        uncertainty[i] = (1 - K) * (uncertainty[i] + proc_var[i])        # updated state uncertainty

