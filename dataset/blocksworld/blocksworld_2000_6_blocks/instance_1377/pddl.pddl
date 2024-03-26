

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(ontable c)
(ontable d)
(on e b)
(clear d)
(clear e)
)
(:goal
(and
(on a d)
(on c e)
(on e b))
)
)


