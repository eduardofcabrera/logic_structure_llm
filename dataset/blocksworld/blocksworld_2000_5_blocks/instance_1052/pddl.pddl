

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(ontable c)
(ontable d)
(on e b)
(clear c)
(clear d)
(clear e)
)
(:goal
(and
(on a c)
(on e d))
)
)


