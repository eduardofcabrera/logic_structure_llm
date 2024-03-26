

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(ontable c)
(on d b)
(on e c)
(clear a)
(clear d)
)
(:goal
(and
(on a b)
(on d e)
(on e c))
)
)


