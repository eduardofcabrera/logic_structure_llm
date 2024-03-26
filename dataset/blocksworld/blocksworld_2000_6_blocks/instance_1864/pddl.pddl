

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(on c a)
(on d b)
(ontable e)
(clear d)
)
(:goal
(and
(on b e)
(on d a))
)
)


