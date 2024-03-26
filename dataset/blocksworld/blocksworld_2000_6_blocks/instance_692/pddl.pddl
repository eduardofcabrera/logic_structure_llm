

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(on c d)
(on d b)
(ontable e)
(clear a)
)
(:goal
(and
(on a c)
(on b a)
(on d b))
)
)


