

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c d)
(on d a)
(ontable e)
(clear c)
(clear e)
)
(:goal
(and
(on b e)
(on d b))
)
)


