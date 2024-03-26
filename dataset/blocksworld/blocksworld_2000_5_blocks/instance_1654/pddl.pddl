

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(ontable d)
(on e c)
(clear a)
(clear b)
(clear d)
(clear e)
)
(:goal
(and
(on a e)
(on e c))
)
)


