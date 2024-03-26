

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(on c d)
(ontable d)
(on e b)
(clear a)
(clear e)
)
(:goal
(and
(on a c)
(on c d)
(on e a))
)
)


