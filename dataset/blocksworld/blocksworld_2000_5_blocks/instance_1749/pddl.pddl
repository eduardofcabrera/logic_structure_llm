

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b e)
(on c a)
(on d b)
(ontable e)
(clear c)
)
(:goal
(and
(on c e)
(on d c)
(on e a))
)
)


