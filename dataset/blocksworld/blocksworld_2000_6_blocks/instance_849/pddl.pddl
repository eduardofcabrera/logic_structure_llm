

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b c)
(on c d)
(ontable d)
(on e a)
(clear e)
)
(:goal
(and
(on a c)
(on b d))
)
)


