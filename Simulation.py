import numpy as np
from matplotlib import pyplot as plt

# Simulation
def supply(A, a, b, d, th, p, g, f, t):
    B = (1 + g) * p * th * ((1 - a) / a) + ((th - t) * g) / (th * f) + p * (1 + b * p + g)
    D = b * p * (1 + d) * (1 - a) * A + b * p * d * a * (A / th)
    E = (p * (th - t) * g) / (f * a * A)
    Rt1wt_wt1 = 2 * E * a * A / (np.sqrt(B ** 2 + 4 * E * D) - B)
    # Eq 10
    coeff = (1 - t) / (1 + b * p * (1 + d) + g)
    return coeff * (1 + b * p + g - b * d / th * Rt1wt_wt1
                    - t * g / (p * th * f) - t * g / (f * Rt1wt_wt1))

def fertility(A, a, b, d, th, p, g, f, t):
    B = (1 + g) * p * th * ((1 - a) / a) + ((th - t) * g) / (th * f) + p * (1 + b * p + g)
    D = b * p * (1 + d) * (1 - a) * A + b * p * d * a * (A / th)
    E = (p * (th - t) * g) / (f * a * A)
    k_ss = ((np.sqrt(B ** 2 + 4 * E * D) - B ) / ( 2 * E )) ** ( 1 / ( 1 - a )) 
    w_ss = (1-a) * A * k_ss ** a
    r_ss = a * A * k_ss ** ( a - 1 )
    K1 = g / (w_ss * f)
    K2 = (1-t) * w_ss
    K3 = (p * (1-t) * th * w_ss) / r_ss
    K4 = 1 + b * p * ( 1 + d ) + g
    return K1 * (( K2 + K3 ) / K4 )

def supply_vs_all(baseline_params, indep_params, param_label):
    for name, val in indep_params.items():
        fig = plt.figure(figsize=(4, 3))
        ax = fig.gca()
        param = baseline_params.copy()
        param[name] = val
        h = supply(**param)
        ax.plot(param[name], h)

        # plot baseline
        base_param, base_val = baseline_params[name], supply(**baseline_params)
        ax.plot(base_param, base_val, marker='o', markersize=5)
        ax.grid(True)
        ax.set_xlabel(f'${param_label[name]}$')
        ax.set_ylabel('$h^*$')
        fig.tight_layout()
        fig.savefig(f'{name}.pdf', bbox_inches='tight')


def supply_vs_fertility_gamma(baseline_params, indep_params):
    fig = plt.figure(figsize=(4, 3))
    ax = fig.gca()
    param = baseline_params.copy()
    param['g'] = indep_params['g']
    h = supply(**param)
    ax.plot(fertility(**param), supply(**param))
    base_param, base_val = fertility(**baseline_params), supply(**baseline_params)
    ax.plot(base_param, base_val, marker='o', markersize=5)
    ax.grid(True)
    ax.set_xlabel(r'$n_{ss}$')
    ax.set_ylabel('$h^*$')
    fig.tight_layout()
    plt.title(r'Labour Supply v. Fertility Through Changing $\gamma$')
    fig.savefig(f'supply-vs-fertility g.pdf', bbox_inches='tight')

def supply_vs_fertility_phi(baseline_params, indep_params):
    fig = plt.figure(figsize=(4, 3))
    ax = fig.gca()
    param = baseline_params.copy()
    param['f'] = indep_params['f']
    h = supply(**param)
    ax.plot(fertility(**param), supply(**param))
    base_param, base_val = fertility(**baseline_params), supply(**baseline_params)
    ax.plot(base_param, base_val, marker='o', markersize=5)
    ax.grid(True)
    ax.set_xlabel(r'$n_{ss}$')
    ax.set_ylabel('$h^*$')
    fig.tight_layout()
    plt.title(r'Labour Supply v. Fertility Through Changing $\phi$')
    fig.savefig(f'supply-vs-fertility f.pdf', bbox_inches='tight')


def robustness_check(baseline_params, indep_params, n_param_sample=50000, n_grad_check=5000, eps=0.01):
    np.random.seed(0)
    n_inconsistent = {p: 0 for p in indep_params}
    for _ in range(n_param_sample):
        # make copy and replace each independent parameter with random value in range
        rand_params = baseline_params.copy()
        rand_params.update({k: np.random.uniform(v.min(), v.max()) for k, v in indep_params.items()})

        # pick an independent parameter to verify and populate with random test points
        for ver_param_name, ver_param_val in indep_params.items():
            tmp_save = rand_params[ver_param_name]
            test_points = np.random.uniform(ver_param_val.min(), ver_param_val.max(), n_grad_check)

            # finite difference at test points
            rand_params[ver_param_name] = np.stack([test_points - eps, test_points + eps])
            result = supply(**rand_params)
            n_pos = np.sum(np.sign(result[1] - result[0]) > 0)
            n_neg = n_grad_check - n_pos
            n_dom = max(n_pos, n_neg)

            # accumulate inconsistency if not all test_points are of the dominant sign
            n_inconsistent[ver_param_name] += n_dom != n_grad_check
            rand_params[ver_param_name] = tmp_save
    return n_inconsistent
        

    # rand_params = 

if __name__ == '__main__':
    baseline_params = {
        'A': 50, 'a': 0.4, 'b': 0.74, 'd': 0.2, 'th': 1.0,
        'p': 0.9, 'g': 0.5923, 'f': 0.2, 't': 0.2
    }
    indep_params = {
        'f': np.linspace(0.15, 0.25), 'g': np.linspace(0.4, 0.8), 't': np.linspace(0.1, 0.5),
        'p': np.linspace(0.8, 1.0), 'th': np.linspace(0.8, 1.2)
    }
    param_label = {'f': '\phi', 'g': r'\gamma', 't': r'\tau', 'p': r'\pi', 'th': r'\theta'}

    plt.rcParams.update({"text.usetex": True, "font.family": "sans-serif"})

    # Plotting
    supply_vs_all(baseline_params, indep_params, param_label)
    supply_vs_fertility_phi(baseline_params, indep_params)
    supply_vs_fertility_gamma(baseline_params, indep_params)


    # Robustness test
    indep_params_update = {
        'f': np.linspace(0.15, 0.25), 'g': np.linspace(0.4, 0.8), 't': np.linspace(0.1, 0.5),
        'p': np.linspace(0.8, 1.0), 'th': np.linspace(0.8, 1.2),
        'b': np.linspace(0.55,1), 'd':np.linspace(0.1,0.3)
    }
    rob_result = robustness_check(baseline_params, indep_params_update, n_param_sample=7000, n_grad_check=7000)
    for k, v in rob_result.items():
        print(f"{v} gradient inconsistencies found for parameter '{k}'")

    plt.show()


