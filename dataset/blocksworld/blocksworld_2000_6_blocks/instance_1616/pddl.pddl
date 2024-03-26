

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(ontable c)
(on d b)
(ontable e)
(clear a)
(clear d)
)
(:goal
(and
(on a c)
(on c e)
(on e b))
)
)


