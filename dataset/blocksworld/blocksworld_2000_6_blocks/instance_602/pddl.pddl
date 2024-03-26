

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b a)
(ontable c)
(ontable d)
(on e b)
(clear c)
(clear e)
)
(:goal
(and
(on a c)
(on b e)
(on c d)
(on e a))
)
)


