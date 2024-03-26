

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(on c d)
(ontable d)
(on e b)
(clear a)
(clear e)
)
(:goal
(and
(on b d)
(on c e))
)
)


