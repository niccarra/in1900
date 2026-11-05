from outbreak import R_to_beta
from pathlib import Path
from datetime import date
import numpy as np
import matplotlib.pyplot as plt


class Beta:
    def __init__(self, filename):
        p = Path(__file__).with_name(filename)
        with p.open() as file:
            # Hopp over de to første linjene
            next(file, None) # Header
            next(file, None) # Understrekke

            self.beta = []
            self.t_start = []
            date_0 = None
            while line := file.readline():
                # Vi antar at alle linjene har gyldig R-verdier og sluttdato
                start_str, _, R = line.split()
                start_date = self.str2date(start_str)
                if date_0 is None:
                    date_0 = start_date
                delta_t = start_date - date_0  
                self.t_start.append(delta_t.days) 
                self.beta.append(R_to_beta(float(R)))  

    def __call__(self, t):
        beta_out = self.beta[0]
        for t_start, beta in zip(self.t_start, self.beta):
            if(t >= t_start):
                beta_out = beta
        return beta_out        

    def plot(self, T):
        t = np.linspace(0, T, 1000)
        beta = np.vectorize(self.__call__)(t)

        plt.plot(t, beta)
    
        plt.title('The time-varying β')
        plt.xlabel('Time (days)')
        plt.ylabel('β')
        plt.show()

    # Hentet fra oppgaveteksten
    def str2date(self, date_str):
        #convert a date string on the format dd.mm.yyyy
        #to a datetime object
        day, month, year = (int(n) for n in date_str.split('.'))
        return date(year,month,day)

def test_Beta():
    beta = Beta('r_values.txt')
    ''' 
    Siste dag i den første perioden: 14.03.2020, eller 28 dager 
    fra 15.02.2020.
    Første dag i den andre perioden: 15.03.2020, eller 29 dager
    fra 15.02.2020

    R for den første perioden: 3.2. beta = 3.2/4.7 ~= 0,6809 
    R for den andre perioden: 0.5, beta = 0.5/4.7 ~= 0.1064

    '''
    np.testing.assert_allclose(beta(28), 0.6809, rtol=1e-04)
    np.testing.assert_allclose(beta(29), 0.1064, rtol=16e-05)

if __name__ == "__main__":
    from SEIR import SEIR, solve_SEIR, plot_SEIR
    test_Beta()
    beta = Beta('r_values.txt')
    beta.plot(600)
    model = SEIR(beta)
    t, u = solve_SEIR(model, T=600, N=600, S_0=5.5e6, E2_0=100)
    plot_SEIR(t, u, components = ['I','Ia'])

    '''
    Hvorfor forutsier ikke modellen flere bølger?
    Vi kan si fra formlene som brukes til å beregne de ulike 
    gruppene (S, I, R) at modellen tar høyde for én enkelt retning 
    som en persons status kan utvikle seg i. Det betyr at når en 
    person blir R = Recovered, de kan ikke bli smittet igjen. Noe
    vi vet var ikke tilfelle under COVID-19. Vi trenger en mer 
    kompliserte modell, for eksempel SIR-SS som også tar hensyn til 
    sosial dynamikk, for å forklare forekomsten av flere smittebølger.
    '''  