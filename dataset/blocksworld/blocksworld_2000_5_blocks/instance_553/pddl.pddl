

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(ontable c)
(on d b)
(ontable e)
(clear a)
(clear d)
(clear e)
)
(:goal
(and
(on b e)
(on c a)
(on d b))
)
)


