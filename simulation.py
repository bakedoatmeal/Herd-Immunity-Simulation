import random, sys
import time
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''

    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.logger = Logger("answers.txt")
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = initial_infected # Int
        self.current_infected = initial_infected # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.vaccinated = 0
        self.total_dead = 0 # Int
        # self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
        #     virus_name, population_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        self.population = self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        new_population = []
        left_to_infect = initial_infected
        left_to_vacc = self.vacc_percentage * self.pop_size
        for index in range(self.pop_size):
            if left_to_vacc > 0:
                new_population.append(Person(index, True, None))
                # print(f"Created new person, {new_population[-1]._id} {new_population[-1].is_vaccinated} {new_population[-1].infection}")
                left_to_vacc -= 1
            elif left_to_infect > 0:
                new_population.append(Person(index, False, self.virus))
                # print(f"Created new person, {new_population[-1]._id} {new_population[-1].is_vaccinated} {new_population[-1].infection}")
                left_to_infect -=1
            else: 
                new_population.append(Person(index, False, None))
                # print(f"Created new person, {new_population[-1]._id} {new_population[-1].is_vaccinated} {new_population[-1].infection}")
        return new_population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # if dead + currently infected + vaccinated == total population, simulation can end.
        total_accounted_for = self.total_dead + self.vaccinated
        if total_accounted_for == self.pop_size:
            print(f"The simulation is ending because everyone is vaccinated or dead")
            return False
        elif len(self.newly_infected) == 0:
            print(f"Herd immunity has been reached!")
            return False
        else:
            return True 

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        time_step_counter = 0
        should_continue = True

        while should_continue:
            self.time_step()
            # self.logger.log_time_step()
            should_continue = self._simulation_should_continue()
            self._infect_newly_infected()
            time_step_counter += 1
            
        print(f'The simulation has ended after {time_step_counter} turns.')

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''

        for person in self.population:
            # if person is alive,
            if person.is_alive:
                # check is person is infected
                if person.infection is not None:
                    # if person is infected, we need to make them interact with 100 people  
                    interaction_counter = 0
                    while interaction_counter < 5:
                        # get one random person to interact with
                        random_person = random.choice(self.population)
                        # find random person that is alive
                        while random_person.is_alive is False: 
                            random_person = random.choice(self.population)
                        # make interaction happen
                        self.interaction(person, random_person)
                        interaction_counter += 1
                    if person.did_survive_infection() is False: 
                        print(f"{person._id} had the disease, they did not survive")
                        self.total_dead += 1
                        self.current_infected -= 1
                        person.is_alive = False
                    else: 
                        print(f"{person._id} has survived and is immune!")
                        self.vaccinated += 1
                        self.current_infected -= 1
                        person.infection = None
                        person.is_vaccinated = True

        print(f"End of a time step! {self.newly_infected} have been infected. Total deaths: {self.total_dead}, total vaccinated: {self.vaccinated}")

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        print(f"Interaction between {person._id} who has {person.infection.name} and {random_person._id} and is vaccinated? {random_person.is_vaccinated} and {random_person.infection}")

        # random_person is vaccinated:
        # nothing happens to random person.
        if random_person.is_vaccinated: 
            pass 
        # random_person is already infected:
        # nothing happens to random person.
        elif random_person.infection is not None:
            pass
        elif random_person._id in self.newly_infected:
            pass
        else: 
            immune_strength = random.random()
            print(immune_strength, self.virus.repro_rate)
            if immune_strength < self.virus.repro_rate:
                self.newly_infected.append(random_person._id)
                print(f"{random_person._id} is infected!")
                self.total_infected += 1
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method
        
        # self.logger.log_interaction()

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for id in self.newly_infected:
            for person in self.population: 
                if person._id == id:
                    person.infection = self.virus
                    print(f"{person._id} is now infected with {person.infection.name}")
        self.newly_infected = []


if __name__ == "__main__":
    # params = sys.argv[1:]
    # virus_name = str(params[0])
    # repro_num = float(params[1])
    # mortality_rate = float(params[2])

    # pop_size = int(params[3])
    # vacc_percentage = float(params[4])

    # if len(params) == 6:
    #     initial_infected = int(params[5])
    # else:
    #     initial_infected = 1

    # virus = Virus(name, repro_rate, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    #sim.run()
    virus = Virus("covid", 0.9, 0.2)
    sim = Simulation(virus, 25, 0.20, 6)
    sim.run()
