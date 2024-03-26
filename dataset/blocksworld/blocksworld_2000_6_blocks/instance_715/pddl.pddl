

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(on c d)
(on d a)
(ontable e)
(clear b)
)
(:goal
(and
(on a b)
(on b e)
(on c a))
)
)


