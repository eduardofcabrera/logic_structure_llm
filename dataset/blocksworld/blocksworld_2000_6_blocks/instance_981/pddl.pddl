

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c d)
(on d b)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on c e)
(on d c)
(on e a))
)
)


