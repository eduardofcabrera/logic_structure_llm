

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(ontable c)
(on d a)
(on e b)
(clear d)
(clear e)
)
(:goal
(and
(on a e)
(on c d)
(on d b)
(on e c))
)
)


