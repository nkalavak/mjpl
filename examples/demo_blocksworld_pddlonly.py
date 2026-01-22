# file to check PDDL logic for blocksworld using PDDLStream
import sys
sys.path.insert(0, '/home/nivii/Desktop/GitHub/pddlstream_local')

from pddlstream.algorithms.meta import solve, create_parser
from pddlstream.language.constants import print_solution, PDDLProblem

# PDDL domain definition for blocksworld
# on - indicates x stacked on y 
DOMAIN_PDDL = """
(define (domain blocksworld)
  (:requirements :strips :equality)
  (:predicates (clear ?x)
               (on-table ?x)
               (arm-empty)
               (holding ?x)
               (on ?x ?y)) 

  (:action pickup
    :parameters (?ob)
    :precondition (and (clear ?ob) (on-table ?ob) (arm-empty))
    :effect (and (holding ?ob) (not (clear ?ob)) (not (on-table ?ob))
                 (not (arm-empty))))

  (:action putdown
    :parameters  (?ob)
    :precondition (and (holding ?ob))
    :effect (and (clear ?ob) (arm-empty) (on-table ?ob)
                 (not (holding ?ob))))

  (:action stack
    :parameters  (?ob ?underob)
    :precondition (and  (clear ?underob) (holding ?ob))
    :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
                 (not (clear ?underob)) (not (holding ?ob))))

  (:action unstack
    :parameters  (?ob ?underob)
    :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
    :effect (and (holding ?ob) (clear ?underob)
                 (not (on ?ob ?underob)) (not (clear ?ob)) (not (arm-empty)))))
"""

def pddl_planning():
    # Initial state: All blocks on table
    init = [
        ('arm-empty',),
        ('clear', 'block_red'),
        ('on-table', 'block_red'),
        ('clear', 'block_blue'),
        ('on-table', 'block_blue'),
        ('clear', 'block_green'),
        ('on-table', 'block_green'),
    ]

    # Goal: Stack blue on red
    goal = ('on', 'block_blue', 'block_red')
    
    print("Initial state:")
    for pred in init:
        print(f"  {pred}")
    print(f"\nGoal: {goal}")
    
    # Create PDDL problem
    constant_map = {}
    stream_pddl = None
    stream_map = {}
    
    problem = PDDLProblem(DOMAIN_PDDL, constant_map, stream_pddl, stream_map, init, goal)
    
    # Solve using PDDLStream
    parser = create_parser()
    args = parser.parse_args([])  # Use default arguments
    
    solution = solve(problem, algorithm=args.algorithm, unit_costs=True, planner='lmcut-astar')
    
    if solution is None:
        print("No solution found!")
        return False
    
    print_solution(solution)
    
    print("\nPlan found:")
    for i, action in enumerate(solution.plan):
        print(f"  {i+1}. {action.name}({', '.join(action.args)})")
    
    return True

if __name__ == "__main__":
    success = pddl_planning()
    if not success:
        sys.exit(1)
    print("\nPDDL planning successful!")