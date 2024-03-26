

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b c)
(ontable c)
(ontable d)
(on e a)
(clear d)
(clear e)
)
(:goal
(and
(on b e)
(on c d))
)
)


