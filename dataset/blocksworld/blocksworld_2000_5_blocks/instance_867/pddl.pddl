

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c a)
(ontable d)
(ontable e)
(clear b)
(clear c)
(clear d)
)
(:goal
(and
(on a c)
(on c d)
(on d b))
)
)


