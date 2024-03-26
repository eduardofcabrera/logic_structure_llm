

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b d)
(on c a)
(ontable d)
(ontable e)
(clear c)
(clear e)
)
(:goal
(and
(on c d)
(on d b)
(on e a))
)
)


