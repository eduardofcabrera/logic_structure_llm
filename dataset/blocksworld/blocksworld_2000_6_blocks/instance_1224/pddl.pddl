

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(on c e)
(on d b)
(ontable e)
(clear d)
)
(:goal
(and
(on d c))
)
)


