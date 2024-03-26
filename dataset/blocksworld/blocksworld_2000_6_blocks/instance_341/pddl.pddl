

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b d)
(on c a)
(on d e)
(ontable e)
(clear c)
)
(:goal
(and
(on a c)
(on b d)
(on c b))
)
)


