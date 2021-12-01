class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''

        outfile = open(self.file_name, "w")
        outfile.write("------------------------------- \n")
        outfile.write(f"Initializing {virus_name} Simulation! \n")
        outfile.write(f"Population size: {pop_size} people, Percent vaccinated: {vacc_percentage * 100}%\n")
        outfile.write(f"Virus mortality rate: {mortality_rate}, Reproduction rate: {basic_repro_num} \n")
        outfile.write("-------------------------------- \n")
        outfile.close()
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file
        

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=False, did_infect=False, newly_infected=False):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        outfile = open(self.file_name, "a")
        if did_infect:
            outfile.write(f"{person._id} infected {random_person._id} \n")
        elif random_person_vacc is True: 
            outfile.write(f"{person._id} did not infect {random_person._id} because they are vaccinated \n")
        elif random_person_sick is not None: 
            outfile.write(f"{person._id} did not infect {random_person._id} because they were already sick \n")
        elif newly_infected:
            outfile.write(f"{person._id} did not infect {random_person._id} because they just got infected \n")
        else: 
            outfile.write(f"{person._id} did not infect {random_person._id} \n")
        outfile.close()

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        outfile = open(self.file_name, "a")
        outfile.write("-------------------CHECKING SURVIVAL----------------------------- \n")
        if did_die_from_infection:
            outfile.write(f"{person._id} died from infection \n")
        else: 
            outfile.write(f"{person._id} survived the infection \n")
        outfile.write("----------------------------------------------------------------- \n")
        outfile.close()

    def log_time_step(self, time_step_number, dead_this_round, newly_vaccinated, current_infected, total_dead, pop_size, vaccinated):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.
            Total number living people, total number of vaccinated people

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        outfile = open(self.file_name, "a")
        outfile.write("\n")
        outfile.write("---------------------END OF TIME STEP---------------------------- \n")
        outfile.write(f"Time step {time_step_number} ended. Analyzing data: \n")
        outfile.write(f"Number of people infected during this time step: {current_infected} \n")
        outfile.write(f"Number of people dead during this time step: {dead_this_round} \n")
        outfile.write(f"Number of people who survived the infection and are now vaccinated: {newly_vaccinated} \n")
        outfile.write(f"Population size: {pop_size}, Total Dead: {total_dead}, Total vaccinated: {vaccinated}, Total infected: {current_infected}\n")
        outfile.write("----------------------------------------------------------------- \n")
        outfile.write("\n")
        outfile.close()


    def endLog(self, message):
        outfile = open(self.file_name, "a")
        outfile.write("\n")
        outfile.write("--------------------END OF SIMULATION---------------------------- \n")
        outfile.write(message)
        outfile.write("\n")
        outfile.close()


