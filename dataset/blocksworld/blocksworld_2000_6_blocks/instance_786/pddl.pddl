

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(ontable d)
(on e a)
(clear c)
(clear d)
(clear e)
)
(:goal
(and
(on a c)
(on b d)
(on e a))
)
)


