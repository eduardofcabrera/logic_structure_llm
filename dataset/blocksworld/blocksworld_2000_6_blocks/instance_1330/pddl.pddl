

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(ontable c)
(ontable d)
(on e b)
(clear a)
(clear c)
(clear e)
)
(:goal
(and
(on a c)
(on c e))
)
)


