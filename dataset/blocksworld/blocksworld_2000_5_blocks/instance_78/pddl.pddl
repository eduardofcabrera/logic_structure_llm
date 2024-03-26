

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b c)
(ontable c)
(on d a)
(ontable e)
(clear d)
(clear e)
)
(:goal
(and
(on a b)
(on b e)
(on e c))
)
)


