

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(on c d)
(on d e)
(ontable e)
(clear b)
)
(:goal
(and
(on a c)
(on b e)
(on d b))
)
)


