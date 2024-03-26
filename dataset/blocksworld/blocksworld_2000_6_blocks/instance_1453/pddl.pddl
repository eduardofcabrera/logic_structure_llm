

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b e)
(on c a)
(on d c)
(ontable e)
(clear d)
)
(:goal
(and
(on c a)
(on e b))
)
)


