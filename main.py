
import string
import random

import genetics

letters = string.ascii_uppercase + string.ascii_lowercase + string.punctuation + ' '
solution = 'Hello World!'


class LetterComponent(genetics.DNAComponent):

    def mutate_value(self):
        return random.choice(letters)


class WordDNA(genetics.arrayed_segment(len(solution), LetterComponent)):

    def score(self):
        score = sum(comp.value == letter for comp, letter in zip(self, solution))
        return score

    def __str__(self):
        return ''.join(comp.value for comp in self)

    def __gt__(self, other):
        return self.score() > other.score()

sim = genetics.DiscreteSimulation(
    population_size=100,
    mutation_mask=genetics.mutation_rate(0.05),  # Mutate at a 5% rate
    crossover_mask=genetics.two_point_crossover,
    selection_function=genetics.tournament(2),
    elite_size=2,
    initial_generator=WordDNA,
    fitness_function=WordDNA.score)


def dna_stats(population):
    '''Best DNA, best score, average score'''
    best_dna = max(population)
    best_score = best_dna.score
    average_score = sum(member.score() for member in population) / len(population)

    return best_dna, best_score, average_score


population = sim.initial_population()

while True:
    best, best_score, average_score = dna_stats(population)

    print('{} | Average score: {}'.format(str(best), average_score))

    if str(best) == solution:
        break

    population = sim.step(population)
