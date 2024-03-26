

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c e)
(on d b)
(ontable e)
(clear a)
(clear c)
(clear d)
)
(:goal
(and
(on a c)
(on c d)
(on d e)
(on e b))
)
)


