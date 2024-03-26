

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(ontable d)
(ontable e)
(clear a)
(clear c)
(clear d)
(clear e)
)
(:goal
(and
(on a b)
(on b c)
(on d a)
(on e d))
)
)


