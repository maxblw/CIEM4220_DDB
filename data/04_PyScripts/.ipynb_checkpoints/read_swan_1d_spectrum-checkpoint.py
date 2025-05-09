import numpy as np

def read_swan_1d_spectrum(file_path):
    """
    Reads a SWAN 1D spectral output file containing:
    - VaDens [m²/Hz]
    - NDIR [deg, nautical]
    - DSPRDEGR [deg]
    
    Returns:
        frequencies : np.ndarray
        vadens      : np.ndarray
        dir_mean    : np.ndarray
        dspred      : np.ndarray
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find frequency section
    freq_idx = next(i for i, line in enumerate(lines) if 'AFREQ' in line)
    nfreq = int(lines[freq_idx + 1].strip().split()[0])
    frequencies = np.array([
        float(lines[freq_idx + 2 + i].strip()) for i in range(nfreq)
    ])

    # Find exception values
    quant_idx = next(i for i, line in enumerate(lines) if 'QUANT' in line)
    vadens_ex = float(lines[quant_idx + 4].split()[0])
    ndir_ex   = float(lines[quant_idx + 7].split()[0])
    dspre_ex  = float(lines[quant_idx + 10].split()[0])

    # Find LOCATION block
    loc_idx = next(i for i, line in enumerate(lines) if line.strip().startswith('LOCATION'))
    spec_start = loc_idx + 1

    vadens, dir_mean, dspred = [], [], []

    for line in lines[spec_start:]:
        parts = line.strip().split()
        if len(parts) != 3:
            continue
        try:
            v, d, s = map(float, parts)
        except ValueError:
            continue
        vadens.append(np.nan if v == vadens_ex else v)
        dir_mean.append(np.nan if d == ndir_ex else d)
        dspred.append(np.nan if s == dspre_ex else s)
        if len(vadens) >= nfreq:
            break

    return (
        np.array(frequencies),
        np.array(vadens),
        np.array(dir_mean),
        np.array(dspred)
    )
