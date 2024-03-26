

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b e)
(on c a)
(ontable d)
(on e c)
(clear b)
)
(:goal
(and
(on a b)
(on c a))
)
)


